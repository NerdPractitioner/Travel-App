import * as actionTypes from "../actions/actionTypes";
import { updateObject } from "../utility";

const initialState = {
  messages: [],
  chats: []
};

const addMessage = (state, action) => {
  return updateObject(state, {
    messages: [...state.messages, action.message]
  });
};

const setMessages = (state, action) => {
  return updateObject(state, {
    messages: action.messages.reverse()
  });
};

const setChats = (state, action) => {
  return updateObject(state, {
    chats: action.chats
  });
};

const reducer = (state = initialState, action) => {
  if(action.type == '@@INIT-APP') {
    // console.log('!', window.__INITIAL_STATE__['chats']);
    let new_s = updateObject(state, {
      chats: window.__INITIAL_STATE__['chats'],
      messages: window.__INITIAL_STATE__['messages'],
    });
    console.log(new_s);
    return new_s;
  }

  switch (action.type) {
    case actionTypes.ADD_MESSAGE:
      return addMessage(state, action);
    case actionTypes.SET_MESSAGES:
      return setMessages(state, action);
    case actionTypes.GET_CHATS_SUCCESS:
      return setChats(state, action);
    default:
      return state;
  }
};

export default reducer;
