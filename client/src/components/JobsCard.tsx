"use client";

import { IJobs } from "@/app/types/job";
import { supabase } from "@/lib/supabase/client";
import { useEffect, useState } from "react";

export default function JobsCard () {
  const [jobs, setJobs] = useState<IJobs[]>([]);
  const [page, setPage] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [viewedJobs, setViewedJobs] = useState<string[]>([]);
  const pageSize = 10;

  const fetchJobs = async (page: number) => {
    const { data, count, error } = await supabase
      .from("job_posts")
      .select("*", { count: "exact" })
      .order("posted_date", { ascending: false })
      .range(page * pageSize, (page + 1) * pageSize - 1)

    if (!error && data) {
      setJobs(data);
      if (count !== null) {
        setTotalPages(Math.ceil(count / pageSize));
      }
    }
  };

  useEffect(() => {
    fetchJobs(page);
  }, [page]);

  useEffect(() => {
    const stored = localStorage.getItem("viewedJobs");
    if (stored) {
      setViewedJobs(JSON.parse(stored));
    }
  }, []);

  const handleClickJob = (link: string) => {
    const updatedViewed = [...new Set([...viewedJobs, link])];
    setViewedJobs(updatedViewed);
    localStorage.setItem("viewedJobs", JSON.stringify(updatedViewed));
  };

  return (
    <div className="grid gap-4">
      {jobs.map((job, idx) => (
        <div
          key={`${job.link}-${idx}`}
          className="border p-4 rounded shadow-sm"
        >
          <h2 className={`text-xl font-bold ${viewedJobs.includes(job.link) ? "text-gray-400" : ""}`}>{job.title}</h2>
          <p className={`text-gray-600 ${viewedJobs.includes(job.link) ? "text-gray-400" : ""}`}>{job.company}</p>
          <p className={`text-sm ${viewedJobs.includes(job.link) ? "text-gray-400" : ""}`}>{job.career} | {job.location}</p>
          <p className="text-xs text-gray-400">{job.source} | {job.posted_date}</p>
          <a
            href={job.link}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 underline mt-2 inline-block"
            onClick={() => handleClickJob(job.link)}
          >
            자세히 보기
          </a>
        </div>
      ))}

      <div className="flex justify-center gap-2 mt-4">
        {Array.from({ length: totalPages }, (_, i) => (
          <button
            key={i}
            onClick={() => setPage(i)}
            className={`px-3 py-1 border rounded ${page === i ? "bg-blue-500 text-white" : "bg-white text-black"}`}
          >
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  );
};