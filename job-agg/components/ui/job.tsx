import Link from "next/link";

export type Jobs = {Company:string, Role:string, Date_Found:string, Location:string, Link:string}
type Props = {job:Jobs[]}


export default function Job({job}:Props) {
    return (
        <div className = "flex flex-col gap-3 justify-center items-center w-full">
            {job.map((posting) => (
                <div key = {posting.Link} className = "intersect:bg-white job w-full h-full bg-zinc-800 rounded-lg flex justify-center items-center text-white text-2xl ">
                    <p className = "h-full w-[10%] flex items-center pl-5">{posting.Company}</p>
                    <p className = "h-full w-[45%] flex items-center pl-5">{posting.Role}</p>
                    <p className = "h-full w-[15%] flex items-center pl-5">{posting.Date_Found}</p>
                    <p className = "h-full w-[20%] flex items-center pl-5">{posting.Location}</p>
                    <p className = "h-full w-[10%] flex items-center pl-5"><Link href={posting.Link} target ="_blank" className = " h-[50%] w-[70%] bg-zinc-600 flex justify-center items-center rounded-lg hover:bg-zinc-500">Apply</Link></p>
                </div>
            ))}
        </div>
    )
}