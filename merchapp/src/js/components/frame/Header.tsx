import React from 'react';
import {Link} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faKey} from '@fortawesome/pro-light-svg-icons';
import {store} from "../../store"
import {observer} from "mobx-react"

export interface IHeaderProps {
    image: string;
    name: string;
}

export const Header = observer((props: IHeaderProps) =>
    <header className="toolbar">
        <div className="container title">
            <img src={props.image}/>
            <Link to="/" className="logo">
                {props.name}
            </Link>
            <div className="right">
                <Link to="/token/" className={"bold vertical-align token" + (store.token ? " valid" : "")}>
                    api token
                    <FontAwesomeIcon style={{margin: '0.1em 0 0 0.3em'}} icon={faKey}/>
                </Link>
            </div>
        </div>
    </header>
);
