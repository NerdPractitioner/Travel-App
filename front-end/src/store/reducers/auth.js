import * as actionTypes from "../actions/actionTypes";
import { updateObject } from "../utility";

const initialState = {
  id: null,
  token: null,
  username: null,
  error: null,
  loading: false
};

const authStart = (state, action) => {
  return updateObject(state, {
    error: null,
    loading: true
  });
};

const authSuccess = (state, action) => {
  return updateObject(state, {
    id: action.id,
    token: action.token,
    username: action.username,
    error: null,
    loading: false
  });
};

const authFail = (state, action) => {
  return updateObject(state, {
    error: action.error,
    loading: false
  });
};

const authLogout = (state, action) => {
  return updateObject(state, {
    token: null,
    username: null
  });
};

const reducer = (state = initialState, action) => {
  if(action.type == '@@INIT-APP') {
      return {
        'id': window.__INITIAL_STATE__['auth']['id'],
        'token': window.__INITIAL_STATE__['auth']['token'],
        'username': window.__INITIAL_STATE__['auth']['username'],
      };
  }

  switch (action.type) {
    case actionTypes.AUTH_START:
      return authStart(state, action);
    case actionTypes.AUTH_SUCCESS:
      return authSuccess(state, action);
    case actionTypes.AUTH_FAIL:
      return authFail(state, action);
    case actionTypes.AUTH_LOGOUT:
      return authLogout(state, action);
    default:
      return state;
  }
};

export default reducer;
