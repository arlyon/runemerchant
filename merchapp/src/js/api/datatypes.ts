/**
 * A price log from the api.
 */
interface ApiPriceLog {
    date: string;

    buy_price: number;
    sell_price: number;
    average_price: number;

    buy_volume: number;
    sell_volume: number;
}

export interface ApiPriceLogWithItemID extends ApiPriceLog {
    item: number;
}

export interface ApiPriceLogWithItem extends ApiPriceLog {
    item: ApiItem;
}

/**
 * An item from the api.
 */
export interface ApiItem {
    item_id: number;
    name: string;
    description: string;
    members: boolean;

    store_price: number;
    buy_limit: number;
    high_alch: number;
}

/**
 * An item with an included price log.
 */
export interface ApiItemWithPriceLog extends ApiItem {
    price: ApiPriceLogWithItemID
}

/**
 * A price log item with favorited.
 */
export interface ApiItemWithPriceLogAndFavorite extends ApiItemWithPriceLog {
    favorited: boolean
}

/**
 * A user from the API.
 */
export interface ApiUser {
    username: string,
    email: string,
    first_name?: string,
    last_name?: string
}

export const hasPriceLog = (item: ApiItem | ApiItemWithPriceLog): item is ApiItemWithPriceLog => {
    return !!(item as ApiItemWithPriceLog).price;
};