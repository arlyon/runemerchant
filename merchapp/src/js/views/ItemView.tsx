import React from 'react';
import {ApiItemWithPriceLogAndFavorite} from "../api/datatypes";
import MerchApi from "../api/MerchApi";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faStar as starOutline} from '@fortawesome/pro-light-svg-icons'
import {faStar as starSolid} from '@fortawesome/pro-solid-svg-icons'
import {Footer} from "../components/frame/Footer";
import {Header} from "../components/frame/Header";
import {FourOFour} from "./404View";

const token = "222cbb20c55024684de0a0b2cf1199de17f034ad";

interface IItemViewProps {
    match: { params: { id: number } }
}

interface IItemViewState {
    missing: boolean
    item: ApiItemWithPriceLogAndFavorite | null
}

export class ItemView extends React.Component<IItemViewProps, IItemViewState> {

    constructor(props: IItemViewProps) {
        super(props);
        this.state = {
            missing: false,
            item: null
        };
        this.getItem()
    }

    public render(props?: {}, state?: {}, context?: any): JSX.Element {
        if (this.state.missing) return <FourOFour/>;

        return (
            <div id="root">
                <Header name="RuneMerchant" image="/logo_black.svg"/>
                <main className="container">
                    {this.state.item != null ? (
                        <div className="verticalContainer">
                            <div className="title">
                                <h1>{this.state.item.name}</h1>
                                <div className="right">
                                    <a className="bold" target="_blank" rel="noopener" href={`http://services.runescape.com/m=itemdb_oldschool/Runescape/viewitem?obj=${this.state.item.item_id}`}>Exchange</a>
                                    <a className="bold" target="_blank" rel="noopener" href={`http://oldschoolrunescape.wikia.com/wiki/${this.state.item.name}`}>Wiki</a>
                                    <div onClick={this.favoriteHandler} style={{marginLeft: "0.2em"}}>
                                        <FontAwesomeIcon icon={this.state.item.favorited ? starSolid : starOutline}/>
                                    </div>
                                </div>
                            </div>
                            <p>{this.state.item.description}</p>
                        </div>
                    ) : null}
                </main>
                <Footer/>
            </div>
        )

    }

    private getItem = async () => {
        const newItem = await MerchApi.getItem(this.props.match.params.id, token);
        if (newItem !== null) this.setState({item: newItem});
        else this.setState({missing: true});
    };

    private favoriteHandler = async (event: any) => {
        if (!this.state.item!.favorited ?
            MerchApi.favoriteItem(this.state.item!.item_id, token) :
            MerchApi.unFavoriteItem(this.state.item!.item_id, token)
        ) {
            const item = this.state.item;
            item!.favorited = !item!.favorited;
            this.setState({item,})
        }
    }
}
