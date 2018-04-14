import * as React from "react";
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
        this.getItems(props.token)
    }

    public render(props?: {}, state?: {}, context?: any) {

        return this.state.items.length ? (
            <section>
                <header><h2>Favorites</h2></header>
                {this.state.items.map((item: ApiItem, index: number) => <ListItem key={index} {...item} />)}
            </section>
        ) : null;
    }


    componentWillReceiveProps(nextProps: Readonly<IFavoritesListProps>, nextContext: any): void {
        this.getItems(nextProps.token)
    }

    private getItems = async (token: string) => {
        this.setState({
            items: await MerchApi.getFavorites(token)
        })
    }
}