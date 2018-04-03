import React from 'react';
import {Footer} from "../components/frame/Footer";
import {Header} from "../components/frame/Header";
import {TokenInput} from "../components/TokenInput";
import {config} from "../config";
import MerchApi from "../api/MerchApi"
import {store} from "../store"
import {observer} from "mobx-react"

@observer
export class TokenView extends React.Component<{}, {}> {

    constructor(props: {}) {
        super(props);
        this.getUser()
    }

    private getUser = async () => {
        if (store.token && !store.user) {
            const user = await MerchApi.getUser(store.token);
            if (user != null) {
                store.setUser(user);
            }
        }
    };

    public render(props?: {}, state?: {}, context?: any): JSX.Element {

        const userData = store.user ? (
            <div className="centered light">
                token registered to {store.user.email} {store.user.first_name && `(${store.user.first_name} ${store.user.last_name})`}
            </div>
        ) : null;

        return (
            <div id="root">
                <Header name="RuneMerchant" image="/logo_black.svg"/>
                <main className="container vertical-container">
                    <h1>Api Token</h1>
                    <p>
                        Adding an api token unlocks a couple of cool features in the app, including
                        favoriting items, adding personal tags, and tracking buy and sell orders.
                        To get the api token associated with the account, you can fill in
                        this <a target="_blank" rel="noopener" href={`${config.apiUrl}/api/v1/auth/login/`}>simple
                        form</a>.
                    </p>
                    <div className="token-container">
                        <TokenInput tokenChanged={this.tokenChanged} token={store.token} />
                    </div>
                    {userData}
                </main>
                <Footer/>
            </div>
        );
    }

    private tokenChanged = async (newToken: string | null) => {
        // fetch user endpoint with token
        if (newToken) {
            const user = await MerchApi.getUser(newToken);
            if (user != null) {
                store.setToken(newToken);
                store.setUser(user);
            }
        } else {
            store.setToken(newToken);
            store.setUser(null);
        }
    }
}
