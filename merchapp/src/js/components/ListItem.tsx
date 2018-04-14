import React from "react";
import {Link} from "react-router-dom";
import {ApiItem, ApiItemWithPriceLog, hasPriceLog} from "../api/datatypes";

export class ListItem extends React.Component<ApiItem | ApiItemWithPriceLog, {}> {
    public render(props?: {}, state?: {}, context?: any) {

        let tags = [];

        if (hasPriceLog(this.props)) {
            tags.push(
                <div key={1} className={"tooltip " + (this.profit() ? "profit" : "loss")}>
                    {this.getProfit()}gp ({this.getPercentage()}%)
                </div>
            );
            tags.push(
                <div key={2} className={"tooltip"}>
                    {this.props.price.buy_price}gp
                </div>
            )
        }

        return (
            <article className="item card">
                <img src={`/icons/${this.props.item_id}.gif`}/>
                <div className="content">
                    <header>
                        <Link to={`/items/${this.props.item_id}/`}>{this.props.name}</Link>
                        <div className="right">
                            {tags}
                            <span className="tag"><span>{this.props.members ? "p2p" : "f2p"}</span></span>
                        </div>
                    </header>
                </div>
            </article>
        );
    }

    private profit = () => hasPriceLog(this.props) ? this.props.price.buy_price < this.props.price.sell_price : null;
    private getProfit = () => hasPriceLog(this.props) ? this.props.price.sell_price - this.props.price.buy_price : null;
    private getPercentage = () => hasPriceLog(this.props) ? ((this.props.price.sell_price / this.props.price.buy_price - 1)* 100).toFixed(2)  : null;
}