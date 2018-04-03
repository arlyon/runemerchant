import React from "react";
import {ApiItem} from "../api/datatypes";
import MerchApi from "../api/MerchApi";
import {ListItem} from "./ListItem";

interface IFavoritesListProps {
    token: string
}

interface IFavoritesListState {
    items: ApiItem[]
}

export class FavoritesList extends React.Component<IFavoritesListProps, IFavoritesListState> {

    constructor(props: IFavoritesListProps) {
        super(props);
        this.state = {
            items: []
        };
        this.getItems()
    }

    public render(props?: {}, state?: {}, context?: any) {

        return this.state.items.length ? (
            <section>
                <header><h2>Favorites</h2></header>
                {this.state.items.map((item: ApiItem) => <ListItem {...item} />)}
            </section>
        ) : null;
    }

    private getItems = async () => {
        this.setState({
            items: await MerchApi.getFavorites(this.props.token)
        })
    }
}