import Link from "next/link"

type Jobs = {Company:string, Role:string, Date_Found:string, Location:string, Link:string}
type Props = {job:Jobs}

export default function Job({job}:Props) {
    return (
        <div className = "w-full h-[13%] bg-zinc-800 rounded-lg flex justify-center items-center">
            <p className = "h-full w-[15%] flex items-center pl-5">{job.Company}</p>
            <p className = "h-full w-[45%] flex items-center pl-5">{job.Role}</p>
            <p className = "h-full w-[15%] flex items-center pl-5">{job.Date_Found}</p>
            <p className = "h-full w-[15%] flex items-center pl-5">{job.Location}</p>
            <p className = "h-full w-[10%] flex items-center pl-5"><Link href={job.Link}>Apply</Link></p>
        </div>
    )
}