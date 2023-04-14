const userId = JSON.parse(document.getElementById('user_id').textContent);
const roomName = JSON.parse(document.getElementById('chat_id').textContent);
const chatId = roomName
let menu_open = false;

function DisplayCurrentTime() {
      let date = new Date();
      let hours = date.getHours() > 12 ? date.getHours() - 12 : date.getHours();
      let am_pm = date.getHours() >= 12 ? "p.m" : "a.m";
      hours = hours < 10 ? "0" + hours : hours;
      let minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
      let time = hours + ":" + minutes + " " + am_pm;
      return time
};

document.getElementById(chatId).classList.toggle("chat-main")


//Web Sockets
const chatSocket = new WebSocket(
  'ws://'
  + window.location.host
  + '/ws/'
  + roomName
  + '/'
)

const SideBarSocket = new WebSocket(
  'ws://'
  + window.location.host
  + '/ws/'
)

chatSocket.onmessage = function(e){
  let data = JSON.parse(e.data)
  console.log(data)
  if(data.type === 'chat') {
      let messages = document.getElementById("messages")
      if (data["author_id"] === userId) {
          console.log(data["author_id"], userId)
          messages.insertAdjacentHTML(
              "beforeend",
              `<div class="message right">
              ${data.message}
              <p class="message-time">${DisplayCurrentTime()}</p>
            </div>`
          )
      } else {
          console.log(data["author_id"], userId)
              messages.insertAdjacentHTML(
                  "beforeend",
                  `
              <div class="message">
                <div class="author">
                  ${data.author_username};
                </div>
                <div>
                  <p>${data.message} </p>
                  <p class="message-time">${DisplayCurrentTime()}</p>
                </div>
              </div>
`
              )
          }
      }

      }

let form = document.getElementById("form")
form.addEventListener("submit", (e) => {
  e.preventDefault()
  let message = e.target.message.value

  let author_id = userId;
  let chat_id = e.target.chat.value

      chatSocket.send(JSON.stringify({
          "message": message,
          "a": author_id,
          "chat": chat_id,
      }))

      SideBarSocket.send(JSON.stringify({
          "message": message,
          "chat": chat_id,
      }))

      form.reset()
})



SideBarSocket.onmessage = function(e){
  let data = JSON.parse(e.data)
  console.log(data)
  if (data["type"] === "new-chat"){

      if (data["users"].includes(userId)){
          let url_img = "/static/icons/img_grey.png";
          let sidebar_block = document.querySelector(".side-bar-content")
          sidebar_block.insertAdjacentHTML(
              "afterbegin",
              `
              <div onclick="location.href='/${data.chat_id}/';" class="chat" id="${data.chat_id}">
        <div class="chat-img">
          <img src="${url_img}" alt="">
        </div>
        <div class="chat-info">
          <div class="chat-top-section">
            <div class="chat-title">
              ${data.title}
            </div>
            <div class="last-msg-time">
              
            </div>
          </div>
          <div class="part-msg">
            
          </div>
        </div>
      </div>
              `
              )
      }
  } else {
      let part_msg = document.getElementById(data["chat_id"]).querySelector(".part-msg")
  console.log(chatId)
  part_msg.innerHTML = data.message

  let time_send = document.getElementById(data["chat_id"]).querySelector(".last-msg-time")
  time_send.innerHTML = DisplayCurrentTime()


  //Change ordering
  let chat_block = document.getElementById(data["chat_id"]);
  let parent = chat_block.parentNode;
  parent.insertBefore(chat_block, parent.firstChild);
  }
}

function menuOpen() {
    menu_open = !menu_open
    document.getElementById("menu").style.display = menu_open ? "block" : "none";
}
