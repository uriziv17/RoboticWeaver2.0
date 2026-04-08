import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Upload, Button, message, Spin, Card } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import type { UploadFile } from "antd";

const UPLOAD_URL = "http://localhost:8000/process";

export default function FileUploader() {
	const [fileList, setFileList] = useState<UploadFile[]>([]);
	const [preview, setPreview] = useState<string | null>(null);
	const [loading, setLoading] = useState(false);
	const navigate = useNavigate();

	const handleFileChange = (info: { fileList: UploadFile[] }) => {
		const file = info.fileList[0];
		setFileList(info.fileList);

		// Generate preview
		if (file?.originFileObj) {
			const reader = new FileReader();
			reader.onload = (e) => {
				setPreview(e.target?.result as string);
			};
			reader.readAsDataURL(file.originFileObj);
		}
	};

	const handleUpload = async () => {
		const file = fileList[0]?.originFileObj;
		if (!file) return;

		setLoading(true);

		try {
			const formData = new FormData();
			formData.append("file", file);

			const response = await fetch(UPLOAD_URL, {
				method: "POST",
				body: formData,
			});

			if (!response.ok) {
				throw new Error(`Upload failed: ${response.statusText}`);
			}

			const data = await response.json();
			const taskId = data.task_id;

			message.success("Upload successful! Redirecting...");
			navigate(`/result/${taskId}`);
		} catch (err) {
			const errorMsg = err instanceof Error ? err.message : "An error occurred";
			alert(errorMsg);
			message.error(errorMsg);
		} finally {
			setLoading(false);
		}
	};

	const Preview = () =>
		!preview ? (
			<></>
		) : (
			<div style={{ textAlign: "center" }}>
				<img
					src={preview}
					alt="Preview"
					style={{
						maxWidth: "100%",
						maxHeight: "300px",
						marginBottom: "20px",
						borderRadius: "8px",
					}}
				/>
				<p style={{ marginBottom: "20px", color: "#666" }}>
					{fileList[0]?.name}
				</p>
				<Button
					type="default"
					onClick={() => {
						setFileList([]);
						setPreview(null);
					}}
					disabled={loading}
					style={{ marginRight: "10px" }}
				>
					Choose Different File
				</Button>
			</div>
		);

	const UploadDialog = () => (
		<Upload.Dragger
			name="file"
			maxCount={1}
			accept="image/*"
			fileList={fileList}
			onChange={handleFileChange}
			disabled={loading}
		>
			<p style={{ fontSize: "18px", marginBottom: "8px" }}>
				<UploadOutlined />
			</p>
			<p style={{ fontSize: "14px" }}>
				Click or drag an image file here to upload
			</p>
		</Upload.Dragger>
	);

	return (
		<div
			style={{
				minHeight: "50vh",
				display: "flex",
				alignItems: "center",
				justifyContent: "center",
				padding: "20px",
			}}
		>
			<Card style={{ width: "100%", maxWidth: "500px" }}>
				<h2 style={{ textAlign: "center", marginBottom: "30px" }}>
					Upload an Image File, and get a weaving simulation!
				</h2>

				<Spin spinning={loading}>
					{!preview ? <UploadDialog /> : <Preview />}
				</Spin>

				<Button
					type="primary"
					size="large"
					block
					onClick={handleUpload}
					disabled={fileList.length === 0 || loading}
					style={{ marginTop: "20px" }}
				>
					{loading ? "Uploading..." : "weave it!"}
				</Button>
			</Card>
		</div>
	);
}
