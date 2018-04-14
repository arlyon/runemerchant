import React from 'react';
import {ApiItemWithPriceLogAndFavorite, ApiPriceLogWithItemID} from "../api/datatypes";
import MerchApi from "../api/MerchApi";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faStar as starOutline} from '@fortawesome/pro-light-svg-icons'
import {faStar as starSolid} from '@fortawesome/pro-solid-svg-icons'
import {Footer} from "../components/frame/Footer";
import {Header} from "../components/frame/Header";
import {TimeChart} from "../components/TimeChart";
import {FourOFour} from "./404View";
import {store} from "../store"
import {observer} from "mobx-react"
import timeago from 'timeago.js';

interface IItemViewProps {
    match: { params: { id: number } }
}

interface IItemViewState {
    missing: boolean
    item: ApiItemWithPriceLogAndFavorite | null
    prices: ApiPriceLogWithItemID[]
}

@observer
export class ItemView extends React.Component<IItemViewProps, IItemViewState> {

    constructor(props: IItemViewProps) {
        super(props);
        this.state = {
            missing: false,
            item: null,
            prices: []
        };

        this.getItem(this.props.match.params.id)
    }

    public render(props?: {}, state?: {}, context?: any): JSX.Element {
        if (this.state.missing) return <FourOFour/>;

        return (
            <div id="root">
                <Header name="RuneMerchant" image="/logo_black.svg"/>
                {this.state.item ? (
                    <main className="container">
                        <header className="title">
                            <h1>{this.state.item.name}</h1>
                            <div className="right">
                                <a className="bold" target="_blank" rel="noopener"
                                   href={`http://services.runescape.com/m=itemdb_oldschool/Runescape/viewitem?obj=${this.state.item.item_id}`}>Exchange</a>
                                <a className="bold" target="_blank" rel="noopener"
                                   href={`http://oldschoolrunescape.wikia.com/wiki/${this.state.item.name}`}>Wiki</a>
                                {store.token &&
                                <div onClick={this.favoriteHandler} style={{marginLeft: "0.2em"}}>
                                    <FontAwesomeIcon
                                        icon={this.state.item.favorited ? starSolid : starOutline}/>
                                </div>}
                            </div>
                        </header>
                        <p>{this.state.item.description}</p>
                        <p>Buy limit: {this.state.item.buy_limit}</p>
                        <p>High alch: {this.state.item.high_alch}</p>
                        <p>Store price: {this.state.item.store_price}</p>
                        <p>High alch: {this.state.item.high_alch}</p>
                        <p>Date: {timeago().format(this.state.item.price.date)}</p>
                        <p>Buy price: {this.state.item.price.buy_price}gp</p>
                        <p>Sell price: {this.state.item.price.sell_price}gp</p>
                        <p>Average price: {this.state.item.price.average_price}gp</p>
                        <p>Buy volume: {this.state.item.price.buy_volume}</p>
                        <p>Sell volume: {this.state.item.price.sell_volume}</p>
                        <TimeChart name="Value (gp)" data={this.convertToPrice(this.state.prices)}/>
                        <TimeChart name="Demand" data={this.convertToDemand(this.state.prices)}/>
                    </main>
                ) : <main />}
                <Footer/>
            </div>
        )
    }

    private getItem = async (id: number) => {
        const newItem = await MerchApi.getItem(id, store.token || undefined);
        if (newItem !== null) {
            this.setState({
                item: newItem,
                prices: await MerchApi.getPriceLogsForItem(id)
            });
        }
        else this.setState({missing: true});
    };

    private favoriteHandler = async (event: any) => {
        if (!this.state.item!.favorited ?
            MerchApi.favoriteItem(this.state.item!.item_id, store.token!) :
            MerchApi.unFavoriteItem(this.state.item!.item_id, store.token!)
        ) {
            const item = this.state.item;
            item!.favorited = !item!.favorited;
            this.setState({item,})
        }
    };

    private convertToPrice = (prices: ApiPriceLogWithItemID[]) => {
        return prices.map(price => {
            return {
                t: new Date(price.date),
                y: price.average_price
            }
        })
    };

    private convertToDemand = (prices: ApiPriceLogWithItemID[]) => {
        return prices.map(price => {
            return {
                t: new Date(price.date),
                y: price.buy_volume / price.sell_volume
            }
        })
    }
}
