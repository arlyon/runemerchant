import React from 'react';
import {Header} from "../frame/header";
import {Link} from 'react-router-dom';

export const FourOFour = () =>
    <div id="root">
        <Header />
        <main id="fourofour">
            <div>
                <img src="/splat.png"/>
                <h1>Sorry. We can't find what you're looking for.</h1>
                <h2><Link to="/">Home Teleport</Link></h2>
            </div>
        </main>
    </div>;
