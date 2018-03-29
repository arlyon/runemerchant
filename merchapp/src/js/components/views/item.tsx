import React from 'react';
import {IItemProps} from "../../api/search";
import {Footer} from "../frame/footer";
import {Header} from "../frame/header";
import {Item} from "../item";
import {Route, Switch} from 'react-router';

interface IItemViewProps {
    id?: number;
    match: any;
}

interface IItemViewState {
    item: IItemProps;
}

export class ItemView extends React.Component<IItemViewProps, IItemViewState> {

    constructor(props: IItemViewProps) {
        super(props);
        this.state = {
            item: {} as IItemProps,
        };
    }

    public render(props?: {}, state?: {}, context?: any): JSX.Element {

        if (this.props.id && this.state.item.item_id != this.props.id) {
            this.getItem(this.props.id);
            return <div />;
        } else {
            return (
                <div id="root">
                    <Header/>
                    <main className="container">
                        <Item {...this.state.item} />
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
