import Image from "next/image";
import Title from "@/components/ui/title";


export default function Home() {
  return (
    <div className="[scrollbar-width:none] flex min-h-screenitems-center bg-black w-full justify-center font-sans overflow-x-hidden overflow-y-scroll">
      <main className="flex min-h-screen w-full flex-col items-center justify-between  px-16 sm:items-start">
        <Title/>
      </main>
    </div>
  );
}
