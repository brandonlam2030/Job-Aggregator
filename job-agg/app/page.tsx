"use client"

import Image from "next/image";
import Title from "@/components/ui/title";
import Job from "@/components/ui/job";
import { useState } from "react";




export default function Home() {
  const [page, changeOffset] = useState(0)
  
  
  return (
    <div className="[scrollbar-width:none] flex min-h-screenitems-center bg-black w-full justify-center font-sans overflow-x-hidden overflow-y-scroll">
      <main className="flex min-h-screen w-full flex-col items-center justify-center  px-16 sm:items-start">
        <Title/>
        <Job/>
      </main>
    </div>
  );
}
