import { Github } from 'lucide-react';
import { Linkedin } from 'lucide-react';
import { Mail } from 'lucide-react';

export default function Footer2() {
    return (
    <div className="mx-auto w-full bg-black px-6 sm:px-8 lg:px-10">
        <footer className="mx-auto w-full">
            <div className="w-full flex flex-col justify-center items-center">
                <ul className = "flex gap-5 items-center justify-center ">
                    <li className = "size-10 flex justify-center items-center rounded-lg bg-neutral-900"><a href = "https://github.com/brandonlam2030/Job-Aggregator" target = "_blank"><Github color = "white" fill = "white" size = {30}/></a></li>
                    <li className = "size-10 bg-neutral-900 rounded-lg flex justify-center items-center"><a href = "https://www.linkedin.com/in/brandonlam2007" target = "_blank"><Linkedin color = "white" fill = "white" size = {30} strokeWidth = {0} /></a></li>
                    <li className = "size-10 bg-neutral-900 rounded-lg flex justify-center items-center"><a href = "https://mail.google.com/mail/?view=cm&to=brandonlam2030@gmail.com" target = "_blank"><Mail color = "white" size = {30} /></a></li>
                </ul>
                <p className = "text-white tracking-tight">© 2026 Brandon Lam. All rights reserved.</p>
            </div>
        </footer>
    </div>
  );
}
