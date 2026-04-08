import { Card } from "antd";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function ResultPage() {
	const { taskId } = useParams<{ taskId: string }>();
	const [resultImage, setResultImage] = useState<File | null>(null);

	// useEffect(() => {
	// 	const getTaskStatus = async () => {
	// 		try {
	// 			const response = await fetch(`http://localhost:8000/status/${taskId}`);
	// 			if (!response.ok) {
	// 				throw new Error(`Failed to fetch result: ${response.statusText}`);
	// 			}
	// 			const data = await response.json();
	// 		}
	// 		catch (err) {
	// 			const errorMsg = err instanceof Error ? err.message : "An error occurred";
	// 			alert(errorMsg);
	// 		}
	// 	};
	// 	getTaskStatus();
	// }, [taskId]);

	return (
		<Card
			title="Result"
			style={{ width: 600, margin: "20px auto", textAlign: "center" }}
		>
			<p>here be result</p>
		</Card>
	);
}
