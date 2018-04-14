import * as React from "react";
import {CachedSearch} from "../api/CachedSearch";
import {ApiItemWithPriceLog} from "../api/datatypes";
import {FavoritesList} from "../components/FavoritesList";
import {ListItem} from "../components/ListItem";
import {TaggedSearchBar} from "../components/TaggedSearchBar";
import {Footer} from "../components/frame/Footer";
import {Header} from "../components/frame/Header";
import {store} from "../store";
import {observer} from "mobx-react"

const placeHolders = [
    "gf",
    "12 trout",
    "max cape",
    "wizard mind blast",
    "burnt lobbies",
    "gold trim",
];

interface ISearchViewState {
    items: ApiItemWithPriceLog[] | null
}

@observer
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

        const items = this.state.items === null ? null :
            this.state.items.length ?
                this.state.items.map((item: ApiItemWithPriceLog, index: number) => <ListItem key={index} {...item} />)
                : <h2 style={{textAlign: 'center', marginTop: '2em'}}>No Matches..</h2>;

        return (
            <div id="root">
                <Header name="RuneMerchant" image="/logo_black.svg"/>
                <main className="container">
                    <TaggedSearchBar
                        searchChanged={this.searchChanged}
                        label="Find an item..."
                        placeholder={this.placeholder}/>
                    {items}
                    {store.token && <FavoritesList token={store.token}/>}
                </main>
                <Footer/>
            </div>
        );
    }

    private searchChanged = async (text?: string, tags?: string[]) => {
        this.setState({
            items: await this.search.getItemByName(text, tags)
        })
    };
}
