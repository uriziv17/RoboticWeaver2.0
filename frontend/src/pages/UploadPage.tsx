import React, { useState } from "react";
import { Typography } from "antd";
import FileUploader from "../components/FileUploader";

export default function UploadPage() {
	return (
		<div style={{ padding: "40px", textAlign: "center" }}>
			<Typography.Title level={1}>
				🖼️ Robotic Weaver Simulator 🤖
			</Typography.Title>
			<FileUploader />
		</div>
	);
}
