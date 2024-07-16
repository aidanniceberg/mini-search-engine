import { SearchResult } from "../interfaces/searchResult";
import { createClient } from "./baseAPIClient";

const client = createClient("http://127.0.0.1:5000/v1");

export const getResults = async (query: string): Promise<SearchResult> => {
    return await client.get<SearchResult>("/search", {
        params: {
            query: query,
        }
    })
        .then(response => response.data);
}
