import * as React from "react";
import {Link} from 'react-router-dom';
import {Header} from "../components/frame/Header";

export const FourOFour = () =>
    <div id="root">
        <Header name="RuneMerchant" image="/logo_black.svg"/>
        <main id="fourofour">
            <div>
                <img src="/splat.png"/>
                <h1>Sorry. We can't find what you're looking for.</h1>
                <h2><Link to="/">Home Teleport</Link></h2>
            </div>
        </main>
    </div>;
