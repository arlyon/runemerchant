import {ApiItem, ApiItemWithPriceLog, ApiPriceLogWithItem, ApiPriceLogWithItemID, ApiUser} from "./datatypes";

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
        const data = await request.json();

        return data as ApiItem[]
    }

    public async getItem(itemId: number) {
        return {} as ApiItemWithPriceLog
    }

    public async getItemByName(name: string, tags?: string[]) {
        const tagstring = tags ? tags.map(tag => "&tag=" + tag).join("") : "";
        const request = await fetch(`${this.base_url}/api/v1/items/?name=${name}${tagstring}`);
        const data = await request.json();

        return data as ApiItem[]
    }

    public async getPrices() {
        return []
    }

    public async getPriceLogsForItem(itemId: number) {
        return []
    }

    public async getFavorites(token: string) {
        return []
    }

    public async favoriteItem(token: string, itemId: number) {
        return false
    };

    public async unFavoriteItem(token: string, itemId: number) {
        return false
    }

    public async getUser() {
        return {} as ApiUser
    }

    public async login(username: string, password: string) {
        return ""
    }
}

interface ItemApi {
    getItems: () => Promise<ApiItem[]>
    getItem: (itemId: number) => Promise<ApiItemWithPriceLog>
    getItemByName: (name: string) => Promise<ApiItem[]>
}

interface PriceApi {
    getPriceLogsForItem: (itemId: number) => Promise<ApiPriceLogWithItemID[]>
    getPrices: () => Promise<ApiPriceLogWithItem[]>
}

interface FavoriteApi {
    favoriteItem: (token: string, itemId: number) => Promise<boolean>
    unFavoriteItem: (token: string, itemId: number) => Promise<boolean>
    getFavorites: (token: string) => Promise<ApiItem[]>
}

interface AuthApi {
    login: (username: string, password: string) => Promise<string>
    getUser: () => Promise<ApiUser>
}

export default new MerchApi("http://localhost:8000");