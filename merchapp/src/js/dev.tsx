import * as React from "react";
import ReactDOM from 'react-dom';
import {App} from "./App";
import {AppContainer} from "react-hot-loader"

import "../scss/style.scss";

const render = (Component: any) => {
    ReactDOM.render(
        <AppContainer>
            <Component/>
        </AppContainer>,
        document.getElementById("app"),
    )
};


function start() {
    render(App);

    // Webpack Hot Module Replacement API
    if ((module as any).hot) {
        (module as any).hot.accept();
    }
}

start();