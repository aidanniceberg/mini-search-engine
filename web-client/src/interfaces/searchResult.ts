export interface SearchResultItem {
    title: string;
    description: string;
    url: string;
}

export interface SearchResult {
    query: string;
    count: number;
    page: number;
    page_size: number;
    items: SearchResultItem[];
}
