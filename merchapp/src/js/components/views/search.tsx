import React from 'react';
import {ApiSearch} from "../../api/search";
import {Footer} from "../frame/footer";
import {Header} from "../frame/header";
import {SearchBar} from "../search";

export class SearchView extends React.Component<{}, {}> {

    private search: ApiSearch;

    constructor(props: {}) {
        super(props);
        this.search = new ApiSearch();
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
