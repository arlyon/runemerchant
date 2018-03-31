import React from "react";
import {Link} from "react-router-dom";
import {ApiItem} from "../api/datatypes";

export class ListItem extends React.Component<ApiItem, {}> {
    public render(props?: {}, state?: {}, context?: any) {
        return (
            <article className="item card">
                <img src={`/icons/${this.props.item_id}.gif`} />
                <div className="content">
                    <header>
                        <Link to={`/items/${this.props.item_id}`}>{this.props.name}</Link>
                        <div className="tags">
                            <span className="tag"><span>{this.props.members ? "p2p" : "f2p"}</span></span>
                        </div>
                    </header>
                </div>
            </article>
        );
    }
}
