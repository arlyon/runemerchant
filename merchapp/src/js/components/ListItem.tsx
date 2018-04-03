import React from "react";
import {Link} from "react-router-dom";
import {ApiItemWithPriceLog} from "../api/datatypes";

export class ListItem extends React.Component<ApiItemWithPriceLog, {}> {
    public render(props?: {}, state?: {}, context?: any) {
        return (
            <article className="item card">
                <img src={`/icons/${this.props.item_id}.gif`}/>
                <div className="content">
                    <header>
                        <Link to={`/items/${this.props.item_id}/`}>{this.props.name}</Link>
                        <div className="right">
                            {this.props.price_log ? (
                                <div className={"tooltip " + (this.profit ? "profit" : "loss")}>
                                    +{this.getProfit()}gp ({this.getPercentage()}%)
                                </div>
                            ) : null}
                            {this.props.price_log ? (
                                <div className={"tooltip"}>
                                    {this.props.price_log.buy_price}gp
                                </div>
                            ) : null}
                            <span className="tag"><span>{this.props.members ? "p2p" : "f2p"}</span></span>
                        </div>
                    </header>
                </div>
            </article>
        );
    }

    private profit = () => this.props.price_log.buy_price < this.props.price_log.sell_price
    private getProfit = () => this.props.price_log.sell_price - this.props.price_log.buy_price
    private getPercentage = () => (this.props.price_log.sell_price / this.props.price_log.buy_price - 1) * 100
}
