import React from 'react';
import {ItemSearch} from "../../api/search";
import {Footer} from "../frame/footer";
import {Header} from "../frame/header";
import {SearchBar} from "../search";

export class SearchView extends React.Component<{}, {}> {

    private search: ItemSearch;

    constructor(props: {}) {
        super(props);
        this.search = new ItemSearch(3);
    }

    public render(props?: {}, state?: {}, context?: any): JSX.Element {
        return (
            <div id="root">
                <Header />
                <main className="container">
                    <SearchBar searchFunction={this.search.getItemByName} label="Find an item..."/>
                </main>
                <Footer />
            </div>
        );
    }
}
