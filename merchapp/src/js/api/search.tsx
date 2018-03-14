import {IItemProps} from "../components/item";

/**
 * A class that searches async but filters any data beyond the first request.
 */
export class ApiSearch {

    private items: IItemProps[];
    private lastSearch: string;

    constructor() {
        this.items = [];
        this.lastSearch = "";
    }

    /**
     * Gets the items from the API with a given name.
     * @param {string} name
     * @returns {Promise<IItemProps[]>}
     */
    public getItemByName = async (name: string): Promise<IItemProps[]> => {

        if (name.length < 3) {
            // don't search if less than 3 characters
            this.items = [];
            this.lastSearch = "";
            return this.items;
        } else if (this.lastSearch !== "" && name.includes(this.lastSearch)) {
            // if three or more, just filter the current set.
            this.lastSearch = name;
            return this.items.filter((item) => item.name.toLowerCase().includes(this.lastSearch.toLowerCase()));
        }

        this.lastSearch = name;
        const response = await fetch(`http://localhost:8000/api/items?search=${name}`);
        this.items = await response.json();

        return this.items;
    }
}
