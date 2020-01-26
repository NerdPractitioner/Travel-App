import React from "react";
import { connect } from "react-redux";
import TimeAgo from 'react-timeago';
import WebSocketInstance from "../websocket";
import Hoc from "../hoc/hoc";

class Chat extends React.Component {
  state = { message: "" };

  initialiseChat() {
    this.waitForSocketConnection(() => {
      // WebSocketInstance.fetchMessages(
      //   this.props.username,
      //   this.props.match.params.chatID
      // );
    });
    WebSocketInstance.connect(this.props.match.params.chatID);
  }

  constructor(props) {
    super(props);
    console.log(props)
    this.initialiseChat();
  }

  waitForSocketConnection(callback) {
    const component = this;
    setTimeout(function() {
      if (WebSocketInstance.state() === 1) {
        console.log("Connection is made");
        callback();
        return;
      } else {
        console.log("wait for connection...");
        component.waitForSocketConnection(callback);
      }
    }, 100);
  }

  messageChangeHandler = event => {
    this.setState({ message: event.target.value });
  };

  sendMessageHandler = e => {
    e.preventDefault();
    const messageObject = {
      from: this.props.username,
      content: this.state.message,
      chatId: this.props.match.params.chatID
    };
    WebSocketInstance.newChatMessage(messageObject);
    this.setState({ message: "" });
  };

  renderMessages = (currentChat, messages) => {
    const currentUserID = this.props.currentUserID;
    return messages.map((message, i, arr) => (
      <li
        key={message.id}
        // style={{ marginBottom: arr.length - 1 === i ? "300px" : "15px" }}
        style={{ marginBottom: arr.length - 1 === i ? "100px" : "15px" }}
        className={message.author.id === currentUserID ? "sent" : "replies"}
      >
        <img
          // src="http://emilcarlsson.se/assets/mikeross.png"
          src={message.author.avatar}
          alt="profile-pic"
        />
        <p>
          <Hoc>
          {currentChat.is_group &&
            <span className="username">{message.author.username}</span>
          }
          </Hoc>
          {message.content}
          <br />
          <small>
            <TimeAgo date={message.timestamp} />
          </small>
        </p>
      </li>
    ));
  };

  scrollToBottom = () => {
    this.messagesEnd.scrollIntoView({ behavior: "smooth" });
  };

  componentDidMount() {
    // this.props.getUserChats(
    //   this.props.username,
    //   this.props.token
    // );
    console.log(
      'Chat.props', this.props
    )
    this.scrollToBottom();
  }

  componentDidUpdate() {
    this.scrollToBottom();
  }

  componentWillReceiveProps(newProps) {
    if (this.props.match.params.chatID !== newProps.match.params.chatID) {
      WebSocketInstance.disconnect();
      this.waitForSocketConnection(() => {
        // WebSocketInstance.fetchMessages(
        //   this.props.username,
        //   newProps.match.params.chatID
        // );
      });
      // WebSocketInstance.connect(newProps.match.params.chatID);
    }
  }

  render() {
    return (
      <Hoc>
        <div className="messages">
          <ul id="chat-log">
            {this.props.messages && this.renderMessages(this.props.currentChat, this.props.messages)}
            <div
              style={{ float: "left", clear: "both" }}
              ref={el => {
                this.messagesEnd = el;
              }}
            />
          </ul>
        </div>
        <div className="message-input">
          <form onSubmit={this.sendMessageHandler}>
            <div className="wrap">
              <input
                onChange={this.messageChangeHandler}
                value={this.state.message}
                required
                id="chat-message-input"
                type="text"
                placeholder="Write your message..."
              />
              {/* <i className="fa fa-paperclip attachment" aria-hidden="true" /> */}
              <button id="chat-message-submit" className="submit">
                <i className="fa fa-paper-plane" aria-hidden="true" />
              </button>
            </div>
          </form>
        </div>
      </Hoc>
    );
  }
}

const mapStateToProps = state => {
  console.log('Chat mapStateToProps:', state);

  let currentChat = null;
  (state.message.chats || []).map(chat => {
    if(chat.id == window.CURRENT_CHAT_ID){
      currentChat = chat;
    }
  });

  return {
    token: state.auth.token,
    currentUserID: state.auth.id,
    username: state.auth.username,

    currentChat: currentChat,
    messages: state.message.messages,
  };
};

export default connect(mapStateToProps)(Chat);
