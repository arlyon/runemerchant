import React from 'react';
import {Link} from 'react-router-dom';

export interface IHeaderProps {
    image: string;
    name: string;
}

export const Header = (props: IHeaderProps) =>
    <header className="toolbar">
        <div className="container">
            <img src={props.image} />
            <Link to="/">
                {props.name}
            </Link>
        </div>
    </header>;
