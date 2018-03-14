import React from 'react';
import {Link} from 'react-router-dom';

export const Header = () =>
    <header className="toolbar">
        <img src="/logo_white.svg"/>
        <Link to="/">
            RuneMerchant
        </Link>
    </header>;
