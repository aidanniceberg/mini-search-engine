import axios from "axios";

export const createClient = (baseURL: string) => {
    const baseClient = axios.create({ baseURL });

    baseClient.interceptors.response.use(response => {
            handleDates(response.data);
            return response;
        },
        error => {
            return Promise.reject(error);
        }
    );

    return baseClient;
};

const handleDates = (body: any) => {
    if (!body || typeof body !== "object") return body;

    for (const key of Object.keys(body)) {
        if (isDateString(body[key])) body[key] = new Date(body[key]);
        else if (typeof body[key] === "object") handleDates(body[key]);
    }
}

const isDateString = (entry: any): boolean => {
    const dateFormat = /^(\w{3}, )(\d{1,2} )(\w{3} )(\d{4} )(\d{2}:){2}(\d{2} )GMT$/;
    return entry && typeof entry === "string" && dateFormat.test(entry);
}
