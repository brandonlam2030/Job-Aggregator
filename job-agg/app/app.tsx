import api from "@/app/api"


const JobPostings = () => {
    const getListings = async (offset:number) => {
        try {
            await api.get("/jobs", {params: {limit:15, offset: {offset}}})
        } catch (error) {
            console.error("No jobs found")
        }
    }

    const getCompanyJobs = async (comapny:string, limit:number, offset:number) => {
        try {
            await api.get(`/jobs/{company}`, {params: {limit:15, offset: {offset}}})
        } catch (error) {
            console.error("No jobs for this company")
        }
    }
}


