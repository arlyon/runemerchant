import React from 'react';
import {ApiItem} from "../api/datatypes";
import {Footer} from "../components/frame/Footer";
import {Header} from "../components/frame/Header";
import {ListItem} from "../components/ListItem";

interface IItemViewProps {
    id?: number;
    match: any;
}

interface IItemViewState {
    item: ApiItem;
}

export class ItemView extends React.Component<IItemViewProps, IItemViewState> {

    constructor(props: IItemViewProps) {
        super(props);
        this.state = {
            item: {} as ApiItem,
        };
    }

    public render(props?: {}, state?: {}, context?: any): JSX.Element {

        if (this.props.id && this.state.item.item_id != this.props.id) {
            this.getItem(this.props.id);
            return <div/>;
        } else {
            return (
                <div id="root">
                    <Header name="RuneMerchant" image="/logo_black.svg"/>
                    <main className="container">
                        <ListItem {...this.state.item} />
                    </main>
                    <Footer/>
                </div>
            );
        }

    }

    private async getItem(id: number) {
        const response = await fetch(`http://localhost:8000/api/items/${id}`);
        const item = await response.json();
        this.setState({item});
    }
}
