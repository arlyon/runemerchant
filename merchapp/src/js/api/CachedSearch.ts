import {ApiItemWithPriceLog} from "./datatypes";
import ApiManager from "./MerchApi";

/**
 * A class that searches async but filters any data beyond the first request.
 */
export class CachedSearch {

    private readonly minCharacters: number;
    private items: ApiItemWithPriceLog[] | null;
    private tags: string[];
    private name: string;

    /**
     * Creates a new instance of the CachedSearch class.
     * @param {number} minCharacters The minimum number of characters.
     */
    constructor(minCharacters: number) {
        this.items = null;
        this.tags = [];
        this.minCharacters = minCharacters;
        this.name = "";
    }

    /**
     * Gets the items from the API with a given name or null if
     * not enough characters were submitted.
     * @param {string} name
     * @param tags
     * @returns {Promise<APIItem[] | null>}
     */
    public getItemByName = async (name=this.name, tags=this.tags): Promise<ApiItemWithPriceLog[] | null> => {

        this.name = name;

        // if more than minimum chars, or a nonempty list of tags
        if (this.name.length > this.minCharacters || (tags && tags.length)) {

            // if the list of tags has changed, get from the server
            if (tags!.length !== this.tags.length) {
                this.tags = tags || [];
                this.items = await ApiManager.getItemsWithPriceByName(this.name, tags);
            }

            // if the items list is not null, filter it instead of fetching
            if (this.items != null) {
                return this.items.filter((item) => item.name.toLowerCase().includes(this.name.toLowerCase()));
            } else {
                this.items = await ApiManager.getItemsWithPriceByName(this.name, tags);
            }
        }
        // search if 3 characters and no tags
        else if (this.name.length == this.minCharacters) {
            this.items = await ApiManager.getItemsWithPriceByName(this.name, tags)
        }
        // invalid search, return null
        else {
            this.items = null;
        }

        return this.items;
    }
}
