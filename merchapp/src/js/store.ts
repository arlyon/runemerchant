import {observable, action, configure} from 'mobx';
import {ApiUser} from "./api/datatypes";

configure({
    enforceActions: true
});

const TOKEN_NAME = "token";

interface IMerch {
    token: string | null
    user: ApiUser | null
}

class Merch implements IMerch{
    @observable token: string | null;
    @observable user: ApiUser | null;

    constructor() {
        this.token = localStorage.getItem(TOKEN_NAME) || null;
        this.user = null;
    }

    @action setToken = (token: string | null) => {
        this.token = token;
        localStorage.setItem(TOKEN_NAME, token || "")
    };

    @action setUser = (user: ApiUser | null) => {
        this.user = user;
    };
}

export const store = new Merch();