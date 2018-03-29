import React from 'react';
import {IItemProps} from "../api/search";
import {Item} from "./item";

export interface ISearchProps {
    label?: string;
    searchFunction: (str: string) => Promise<IItemProps[] | null>;
}

interface ISearchState {
    text: string;
    items: IItemProps[] | null;
}

const placeHolders = [
    "gf",
    "12 trout",
    "max cape",
    "wizard mind blast",
    "burnt lobbies",
    "gold trim",
];

export class SearchBar extends React.Component<ISearchProps, ISearchState> {

    constructor(props: ISearchProps) {
        super(props);
        this.state = {
            items: [],
            text: "",
        } as ISearchState;
    }

    private handleChange = async (event: React.FormEvent<HTMLInputElement>) => {

        const text = event.currentTarget.value;
        const items = await this.props.searchFunction(text);

        this.setState({
            text,
            items: items ? items : [],
        });
    };

    public render(props?: ISearchProps, state?: {}, context?: any): JSX.Element {

        let items = null;

        if (this.state.items) {
            items = this.state.items.map((item: IItemProps) => <Item key={item.item_id} {...item} />);
        }


        return (
            <div className="search">
                <input
                    placeholder={"Buying " + placeHolders[Math.floor(Math.random() * placeHolders.length)]}
                    onChange={this.handleChange}
                    value={this.state.text}
                />
                {items}
            </div>
        );
    }
}
