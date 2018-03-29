export interface IItemProps {
    item_id: number;
    name: string;
}

/**
 * A class that searches async but filters any data beyond the first request.
 */
export class ItemSearch {

    private items: IItemProps[] | null;
    private lastSearch: string;
    private characters: number;

    /**
     * Creates a new instance of the ItemSearch class.
     * @param {number} characters The minimum number of characters.
     */
    constructor(characters: number) {
        this.items = [];
        this.lastSearch = "";
        this.characters = characters;
    }

    /**
     * Gets the items from the API with a given name or null if
     * not enough characters were submitted.
     * @param {string} name
     * @returns {Promise<IItemProps[] | null>}
     */
    public getItemByName = async (name: string): Promise<IItemProps[] | null> => {

        if (name.length < this.characters) {
            // don't search if less than 3 characters
            this.items = null;
            this.lastSearch = "";
            return this.items;
        } else if (this.lastSearch !== "" && name.includes(this.lastSearch)) {
            // if three or more, just filter the current set.
            this.lastSearch = name;
            return this.items ? this.items.filter((item) => item.name.toLowerCase().includes(this.lastSearch.toLowerCase())) : null
        }

        this.lastSearch = name;
        const response = await fetch(`http://localhost:8000/api/v1.0/items?search=${name}`);
        this.items = await response.json();

        return this.items;
    }
}
