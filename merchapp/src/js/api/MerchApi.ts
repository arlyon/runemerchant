import {
    ApiItem,
    ApiItemWithPriceLog,
    ApiItemWithPriceLogAndFavorite,
    ApiPriceLogWithItem,
    ApiPriceLogWithItemID,
    ApiUser
} from "./datatypes";

/**
 * A set of functions for interacting with the MerchApi
 */
class MerchApi implements ItemApi, PriceApi, FavoriteApi, AuthApi {

    private readonly base_url: string;

    constructor(base_url: string) {
        this.base_url = base_url;
    }

    public async getItems() {
        const request = await fetch(`${this.base_url}/api/v1/items/`);
        return await request.json();
    }

    public async getItem(itemId: number, token?: string) {
        const headers = token ? new Headers({Authorization: `Token ${token}`}) : undefined;
        const request = await fetch(`${this.base_url}/api/v1/items/${itemId}/`, {headers,});
        return request.status === 404 ? null : await request.json()
    }

    public async getItemsByName(name: string, tags?: string[]) {
        const tagString = tags ? tags.map(tag => "&tag=" + tag).join("") : "";
        const request = await fetch(`${this.base_url}/api/v1/items/?name=${name}${tagString}`);
        return await request.json()
    }

    public async getItemsWithPriceByName(name: string, tags?: string[]) {
        const tagString = tags ? tags.map(tag => "&tag=" + tag).join("") : "";
        const request = await fetch(`${this.base_url}/api/v1/items/?name=${name}${tagString}&prices=true`);
        return await request.json()
    }

    public async getPrices() {
        const request = await fetch(`${this.base_url}/api/v1/prices/`);
        return await request.json()
    }

    public async getPriceLogsForItem(itemId: number) {
        const request = await fetch(`${this.base_url}/api/v1/items/${itemId}/prices/`);
        return request.status === 404 ? null : await request.json()
    }

    public async getFavorites(token: string) {
        const headers = new Headers({Authorization: `Token ${token}`});
        const request = await fetch(`${this.base_url}/api/v1/favorites/`, {headers,});
        return await request.json()
    }

    public async favoriteItem(itemId: number, token: string) {
        const headers = new Headers({Authorization: `Token ${token}`});
        const request = await fetch(`${this.base_url}/api/v1/items/${itemId}/favorite/`, {
            headers,
            method: 'POST'
        });
        return request.status == 201
    };

    public async unFavoriteItem(itemId: number, token: string) {
        const headers = new Headers({authorization: `Token ${token}`});
        const request = await fetch(`${this.base_url}/api/v1/items/${itemId}/favorite/`, {
            headers,
            method: 'DELETE'
        });
        return request.status == 204
    }

    public async getUser(token: string) {
        const headers = new Headers({authorization: `Token ${token}`});
        const request = await fetch(`${this.base_url}/api/v1/auth/user/`, {
            headers,
        });

        return request.status == 200 ? await request.json() : null
    }

    public async login(username: string, password: string) {
        return ""
    }
}

interface ItemApi {
    getItems: () => Promise<ApiItem[]>

    /**
     * Gets the item corresponding to the given id, or null if the id is invalid.
     * @param {number} itemId
     * @param {string} token If included, adds the favorited status to the item.
     * @returns {Promise<ApiItemWithPriceLog | ApiItemWithPriceLogAndFavorite | null>}
     */
    getItem: (itemId: number, token?: string) => Promise<ApiItemWithPriceLog | ApiItemWithPriceLogAndFavorite | null>

    getItemsByName: (name: string, tags?: string[]) => Promise<ApiItem[]>
    getItemsWithPriceByName: (name: string, tags?: string[]) => Promise<ApiItemWithPriceLog[]>
}

interface PriceApi {
    getPriceLogsForItem: (itemId: number) => Promise<ApiPriceLogWithItemID[] | null>
    getPrices: () => Promise<ApiPriceLogWithItem[]>
}

interface FavoriteApi {
    favoriteItem: (itemId: number, token: string) => Promise<boolean | null>
    unFavoriteItem: (itemId: number, token: string) => Promise<boolean | null>
    getFavorites: (token: string) => Promise<ApiItem[]>
}

interface AuthApi {
    login: (username: string, password: string) => Promise<string | null>
    getUser: (token: string) => Promise<ApiUser | null>
}

export default new MerchApi(API_URL);