import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { withRouter } from "react-router-dom";
import Hoc from "../hoc/hoc";

class Profile extends React.Component {
  render() {
    // console.log('profile.props', this.props);
    // this.props.match.params.chatID

    let targetUser = null;
    (this.props.chats || []).map(chat => {
      if(chat.id == window.CURRENT_CHAT_ID){
        chat.participants.map(p => {
          if(p.id != this.props.currentUserID){
            targetUser = p;
          }
        })
      }
    })

    console.log('this.props.currentUserID', this.props.currentUserID);
    console.log('targetUser', targetUser);

    if (this.props.token === null) {
      // return <Redirect to="/" />;
      return <div>Missing auth token</div>;
    }
    if(targetUser === null){
      return <div></div>;
    }

    return (
      <div className="contact-profile">
        {targetUser.username !== null ? (
          <Hoc>
            {/* <img src="http://emilcarlsson.se/assets/harveyspecter.png" alt="" /> */}
            <img src={ targetUser.avatar } alt={targetUser.username} />
            <p>{targetUser.username}</p>
            {/* <div className="social-media">
              <i className="fa fa-facebook" aria-hidden="true" />
              <i className="fa fa-twitter" aria-hidden="true" />
              <i className="fa fa-instagram" aria-hidden="true" />
            </div> */}
          </Hoc>
        ) : null}
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    token: state.auth.token,
    currentUserID: state.auth.id,
    username: state.auth.username,
    chats: state.message.chats
  };
};

export default withRouter(
  connect(mapStateToProps)(Profile)
  );
