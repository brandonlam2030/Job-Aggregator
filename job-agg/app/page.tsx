"use client"

import Title from "@/components/ui/title";
import Job from "@/components/ui/job";
import { useEffect, useState } from "react";
import api from "@/app/api";
import {Jobs} from "@/components/ui/job";



export default function Home() {
  const [page, changeOffset] = useState(0)

  const moreJobs = (() => (
    changeOffset(page+10)
  ))
  const [jobs, setJobs] = useState<Jobs[]>([])
  
  useEffect(() => {
    const fetchJobs = async () => {
      const response = await api.get(`/api/jobs?offset=${page}` )
      setJobs(prev => [...prev, ...response.data])
    }
    fetchJobs()
  }, [page])
  
  return (
    <div className="overscroll-none flex items-center bg-black w-full justify-center font-sans ">
      <main className="flex w-full flex-col items-center justify-start py-16 px-16 gap-5">
        <Title/>
        <Job job = {jobs}/>
        <button onClick = {moreJobs} className = "flex items-center justify-center w-[10%] p-2 rounded-lg text-white text-2xl hover:bg-zinc-700">Load More</button>
      </main>
    </div>
  );
}
