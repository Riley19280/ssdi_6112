import json
import errno
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
# import seaborn as sns
import os
from django.conf import settings
matplotlib.use('agg')


def generate_graphs(user, dataset_name, file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        dataset = pd.DataFrame({
            "name": [x['sender_name'] if 'sender_name' in x else 'no_name' for x in data['messages']],
            "timestamp": [x['timestamp_ms'] for x in data['messages']],
            "message": ['' if 'content' not in x else x['content'] for x in data['messages']],
            "type": [x['type'] for x in data['messages']],
            "photo": [True if 'photos' in x else False for x in data['messages']],
            "gif": [True if 'gifs' in x else False for x in data['messages']],
            "share": [True if 'share' in x else False for x in data['messages']]
        })
    dataset['timestamp'] = pd.to_datetime(dataset['timestamp'], errors='coerce', unit='ms', utc=True)
    join_counts(user, dataset_name, dataset)
    message_counts(user, dataset_name, dataset)
    active_days(user, dataset_name, dataset)
    gif_count(user, dataset_name, dataset)
    gif_to_msg_ratio(user, dataset_name, dataset)


def join_counts(user, dataset_name, dataset):
    filepath = get_save_path(user, dataset_name, 'join_counts.svg')

    df = dataset.loc[dataset['type'] == 'Subscribe'][::-1].reset_index()
    df['index'] = [x for x in range(len(df['name']))]
    ax = df.plot(x='timestamp', y='index', figsize=(15,5), linewidth=5, fontsize=20)
    ax.set_xlabel("Date", fontsize=20)
    ax.set_ylabel("Increased member count", fontsize=20)
    ax.legend(["Member Increase"]);
    plt.xticks(fontsize=20)

    plt.tight_layout()
    plt.savefig(filepath)


def message_counts(user, dataset_name, dataset):
    filepath = get_save_path(user, dataset_name, 'message_count.svg')

    df = dataset.groupby('name').size().reset_index()
    df.columns = ['name', 'count']
    df.sort_values('count', ascending=False, inplace=True)
    ax = df.head(10).plot.bar(x='name', figsize=(15,5), fontsize=15, rot=55)
    ax.set_ylabel("Messages sent", fontsize=20)
    ax.set_xlabel("Names", fontsize=20)

    plt.tight_layout()
    plt.savefig(filepath)


def active_days(user, dataset_name, dataset):
    filepath = get_save_path(user, dataset_name, 'active_days.svg')

    weekdays(dataset, 'All')

    plt.tight_layout()
    plt.savefig(filepath)


def gif_count(user, dataset_name, dataset):
    filepath = get_save_path(user, dataset_name, 'gif_count.svg')

    df_gif = dataset.loc[dataset['gif'] == True].groupby('name').size().reset_index()
    df_gif.columns= ['name', 'count']
    df_gif.sort_values('count', ascending=False, inplace=True)
    ax = df_gif.head(10).plot.bar(x='name', figsize=(10,5), fontsize=15, rot=55)
    ax.set_ylabel("Gifs sent", fontsize=20)
    ax.set_xlabel("Names", fontsize=20)

    plt.tight_layout()
    plt.savefig(filepath)


def gif_to_msg_ratio(user, dataset_name, dataset):
    filepath = get_save_path(user, dataset_name, 'gif_to_msg_ratio.svg')

    df_gif = dataset.loc[dataset['gif'] == True].groupby('name').size().reset_index()
    df_messages = dataset.loc[dataset['gif'] == False].groupby('name').size().reset_index()
    df_gif.columns= ['name', 'count_gif']
    df_messages.columns= ['name', 'count_msg']
    df = df_messages.merge(df_gif, left_on='name', right_on='name')

    # df['ratio'] = [x['count_gif'] / x['count_msg'] for x in df]
    df['ratio'] = [df['count_gif'][x] / df['count_msg'][x] for x in range(len(df['name']))]

    df.sort_values('ratio', ascending=False, inplace=True)
    ax = df.head(10).plot.bar(x='name', y='ratio', figsize=(10,5), fontsize=15, rot=65)
    ax.set_ylabel("Gif to message ratio", fontsize=20)
    ax.set_xlabel("Names", fontsize=20)

    plt.tight_layout()
    plt.savefig(filepath)


def get_save_path(user, dataset_name, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, 'graphs', str(user.id), dataset_name, filename)

    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath), mode=0o777)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return filepath


def weekdays(df, title):
    df['day'] = df['timestamp'].dt.dayofweek
    df = df.groupby('day').size().reset_index(name='counts')

    days = ['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Suunday']
    df['day'] = [days[x] for x in df['day']]
    ax = df.plot.bar(x='day', y='counts', figsize=(15,5), fontsize=20, rot=60)
    ax.set_ylabel("Messages sent", fontsize=20)
    ax.set_xlabel("Day of week - " + title, fontsize=20)
    return ax