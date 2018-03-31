import React from 'react';
import {CachedSearch} from "../api/CachedSearch";
import {ApiItem} from "../api/datatypes";
import {ListItem} from "../components/ListItem";
import {TaggedSearchBar} from "../components/TaggedSearchBar";
import {Footer} from "../components/frame/Footer";
import {Header} from "../components/frame/Header";

const placeHolders = [
    "gf",
    "12 trout",
    "max cape",
    "wizard mind blast",
    "burnt lobbies",
    "gold trim",
];

interface ISearchViewState {
    items: ApiItem[]
}

export class SearchView extends React.Component<{}, ISearchViewState> {

    private search: CachedSearch;
    private placeholder = placeHolders[Math.floor(Math.random() * placeHolders.length)];

    constructor(props: {}) {
        super(props);
        this.search = new CachedSearch(3);
        this.state = {
            items: []
        }
    }

    public render(props?: {}, state?: {}, context?: any): JSX.Element {

        const items = this.state.items.map(
            (item, index: number) => <ListItem key={index} {...item} />
        );

        return (
            <div id="root">
                <Header name="RuneMerchant" image="/logo_black.svg"/>
                <main className="container">
                    <div className="searchContainer">
                        <TaggedSearchBar
                            searchChanged={this.searchChanged}
                            label="Find an item..."
                            placeholder={this.placeholder}/>
                        {items}
                    </div>
                </main>
                <Footer/>
            </div>
        );
    }

    private searchChanged = async (text?: string, tags?: string[]) => {
        this.setState({
            items: await this.search.getItemByName(text, tags) || []
        })
    };
}
