import {observable, action, configure} from 'mobx';
import {ApiUser} from "./api/datatypes";

configure({
    enforceActions: true
});

const TOKEN_KEY = "token";
const USER_KEY = "user";

interface IMerch {
    token: string | null
    user: ApiUser | null
}

class Merch implements IMerch {
    @observable token: string | null;
    @observable user: ApiUser | null;

    constructor() {
        this.token = localStorage.getItem(TOKEN_KEY) || null;
        this.user = localStorage.getItem(USER_KEY) ? JSON.parse(atob(localStorage.getItem(USER_KEY)!)) : null;
    }

    @action setToken = (token: string | null) => {
        this.token = token;
        localStorage.setItem(TOKEN_KEY, token || "")
    };

    @action setUser = (user: ApiUser | null) => {
        this.user = user;
        localStorage.setItem(USER_KEY, btoa(JSON.stringify(user)))
    };
}

export const store = new Merch();

window.addEventListener('storage', (event: StorageEvent) => {
    if (event.key == TOKEN_KEY && event.newValue != store.token) {
        store.setToken(event.newValue || null);
    }
    if (event.key == USER_KEY && btoa(JSON.stringify(store.user)) != event.newValue) {
        store.setUser(JSON.parse(atob(localStorage.getItem(USER_KEY) || "")))
    }
});