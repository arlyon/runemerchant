import React from "react";
import {Link} from "react-router-dom";

export interface IItemProps {
    item_id: number;
    name: string;
}

export class Item extends React.Component<IItemProps, {}> {
    public render(props?: {}, state?: {}, context?: any): JSX.Element {
        return (
            <article className="item card">
                <header><Link to={`/items/${this.props.item_id}`}>{this.props.item_id} {this.props.name}</Link></header>
            </article>
        );
    }
}
