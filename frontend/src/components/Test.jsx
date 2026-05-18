import { DayPicker } from "react-day-picker";
import { useState } from "react";
import "react-day-picker/style.css";
// asas
function Test() {
	const [date, setDate] = useState(new Date());
	const startDate = new Date(2026, 3, 7);

	return (
		<>
			<div className="flex flex-col items-center">
				<DayPicker
					classNames={{
						month: "bg-indigo-50 p-5 rounded-xl shadow",
						button_next: "mt-10 mr-8",
						button_previous: "mt-10",
						day_button:"size-8 ",
						day: "size-5 text-xs ",
						head_cell: "size-5 font-medium text-xs",
						month_grid: "size-5 border-separate border-spacing-2",
						caption_label: "text-xl mt-2 font-bold",
						nav_button: "h-10 w-10",
						week_number_header: "text-xs",
						weekday: "text-sm ",
						MonthsDropdown:"bg-blue-200"
					}}
					captionLayout="label"
					mode="single"
					noonSafe
					fixedWeeks 
					numberOfMonths={1}
					showOutsideDays
					timeZone="Asia/Jakarta"
					weekStartsOn={0}
					onSelect={setDate}
					selected={date}
					disabled={[
						{ dayOfWeek: [0, 6] },
						{ before: startDate },
						{ after: new Date() },
					]}
					modifiers={{
						afterStartDate: (date) => {
							const isAfterStart = date > startDate;
							const isWeekend =
								date.getDay() === 0 || date.getDay() === 6;
							const isBeforeToday = date < new Date();
							return isAfterStart && isBeforeToday && !isWeekend;
						},
						beforeStartDate: { before: new Date(2026, 1, 1) },
					}}
					modifiersClassNames={{
						selected: "!bg-sky-500 text-white rounded-full",
						today: "font-bold !bg-sky-900 !text-white ring-3 ring-sky-900 ring-offset-1 ring-offset-white rounded-full underline",
						beforeStartDate: "text-slate-500",
						afterStartDate: "bg-slate-200 text-black rounded-full",
					}}
				/>
				<p>
					Selected Date: {date ? date.toLocaleDateString() : "None"}
				</p>
			</div>
		</>
	);
}

export default Test;
