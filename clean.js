const fs = require('fs-extra')
const path = require('path')
const faker = require('faker')

let args = process.argv.slice(2);
if(!args[0])
    return console.error(`No message file supplied.`)
if(!fs.pathExistsSync(path.join(__dirname, args[0])))
    return console.error(`Message file not found at ${path.join(__dirname, args[0])}`)


let file_text = fs.readFileSync(path.join(__dirname, args[0]), 'utf8');
//prevent unicode encodings from being converted into actual characters. The characters are unreadable
file_text = file_text.replace(/\\u/g, '\\\\u')

// const message_file = fs.readJsonSync(path.join(__dirname, args[0]))
const message_file = JSON.parse(file_text)

if(!message_file.participants || !message_file.messages || !message_file.title || !message_file.is_still_participant || !message_file.thread_type || !message_file.thread_path ) {
    return console.error('Integrity of the message file is not correct.')
}

const nameIndex = message_file.participants.reduce(function (a, x) {
    a[x.name] = faker.name.findName()
    return a
}, {})

message_file.title = 'Chat Title'
message_file.thread_path = 'thread/path'
message_file.is_still_participant = true
for(let participant of message_file.participants) {
    participant.name = nameIndex[participant.name]
}


for(let message of message_file.messages) {
    message.sender_name = nameIndex[message.sender_name]
    if(message.reactions) {
        for(let reaction of message.reactions) {
            reaction.actor = nameIndex[reaction.actor]
        }
    }
    if(message.photos) {
        for(let photo of message.photos) {
            photo.uri = 'uri/redacted'
        }
    }
    if(message.gifs) {
        for(let gif of message.gifs) {
            gif.uri = 'uri/redacted'
        }
    }
    if(message.videos) {
        for(let video of message.videos) {
            video.uri = 'uri/redacted'
            video.thumbnail.uri = 'uri/redacted'
        }
    }
    if(message.sticker) {
        message.sticker.uri = 'uri/redacted'
    }
    if(message.share) {
        message.share.link = 'uri/redacted'
        message.content = 'uri/redacted'
    }
    if(message.content && message.type === 'Generic') {
        const regex = /(?<!\\)\b(?:\w|')+/gm;
        message.content = message.content.replace(regex, faker.lorem.word)

    }
    if(message.users) {
        for(let user of message.users) {
            user.name = nameIndex[user.name]

        }
    }

    let handled_keys = ['sender_name', 'timestamp_ms', 'content', 'type', 'reactions', 'photos', 'gifs', 'videos', 'sticker', 'share', 'users']
    for(let message_key of Object.keys(message))
        if(!handled_keys.includes(message_key))
            console.error(`message key not handled: ${message_key}`)
}

fs.outputJsonSync('./example_2_messages.json', message_file, { spaces: 4 })