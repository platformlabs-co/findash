import Card from "components/card";
import React, { useEffect, useState } from 'react';
import ComplexTable from "./ComplexTable";
import tableDataComplex from "./../variables/tableDataComplex"
import { CallBackendService } from "utils";
import { useAuth0 } from "@auth0/auth0-react";

const VendorMetrics = (props: { vendorName: String }) => {
  const [data, setData] = useState<string | null>(null);
  const {  getAccessTokenSilently } = useAuth0();
  const [error, setError] = useState<string | null>(null);


  useEffect(() => {
    const fetchData = async () => {
      try {
        const backend_data = await CallBackendService(`/v1/vendors-metrics/${props.vendorName.toLowerCase()}`, getAccessTokenSilently);
        console.log(backend_data);
        setData(backend_data);
      } catch (error) {	
        console.error(error);
        setError('Failed to fetch vendor metrics');
      }
    };
    fetchData();
  }, [props.vendorName]);
  return (
    <Card extra="pb-10 p-[20px]">
      <h1 className="uppercase text-cemter font-bold title">{props.vendorName}</h1>
      <ComplexTable tableData={tableDataComplex}/> 
    </Card>
  );
};

export default VendorMetrics;
