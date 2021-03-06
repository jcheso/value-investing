import { gql } from "@apollo/client";
import client from "./api/apollo-client";
import Layout from "../components/layout";
import { useTable, useSortBy } from "react-table";
import React from "react";
import { useMemo } from "react";
import Head from "next/head";
import {
  TiArrowUnsorted,
  TiArrowSortedUp,
  TiArrowSortedDown,
} from "react-icons/ti";

// import InvestingForm from "../components/investing-form";

const MagicFormula = (props) => {
  const data = React.useMemo(() => props.data.magicFormulaScore, []);

  const columns = React.useMemo(
    () => [
      {
        Header: "Symbol",
        accessor: "symbol", // accessor is the "key" in the data
      },
      {
        Header: "Company Name",
        accessor: "companyName",
      },
      {
        Header: "Sector",
        accessor: "sector",
      },
      {
        Header: "Industry",
        accessor: "industry",
      },
      {
        Header: "Score",
        accessor: "magicFormulaRank",
      },
    ],
    []
  );

  // Create table with useSortBy function
  const tableInstance = useTable({ columns, data }, useSortBy);

  // Create React Table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    tableInstance;

  return (
    <>
      <Head>
        <title>Magic Formula</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <Layout
        title="Magic Formula"
        description="Magic formula investing refers to a rules-based, disciplined investing strategy that teaches people a relatively simple and easy-to-understand method for value investing. It relies on quantitative screens of companies and stocks, and is designed to beat the stock market's average annual returns using the S&P 500 to represent the market return. Put simply, it works by ranking stocks based on their price and returns on capital."
        updated="Last Updated: 06/09/2021"
      >
        <div className="flex flex-col ">
          <div className="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
              <div className="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg h-vh overflow-y-scroll">
                <table
                  className="min-w-full divide-y divide-gray-200"
                  {...getTableProps()}
                >
                  <thead>
                    {headerGroups.map((headerGroup, index) => (
                      <tr key={index} {...headerGroup.getHeaderGroupProps()}>
                        {headerGroup.headers.map((column, index) => (
                          <th
                            key={index}
                            {...column.getHeaderProps(
                              column.getSortByToggleProps()
                            )}
                            scope="col"
                            className="sticky top-0 px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50"
                          >
                            <div className="flex flex-row items-center">
                              {column.render("Header")}
                              <span className="pl-1">
                                {column.isSorted ? (
                                  column.isSortedDesc ? (
                                    <TiArrowSortedDown />
                                  ) : (
                                    <TiArrowSortedUp />
                                  )
                                ) : (
                                  <TiArrowUnsorted />
                                )}
                              </span>
                            </div>
                          </th>
                        ))}
                      </tr>
                    ))}
                  </thead>
                  <tbody {...getTableBodyProps()}>
                    {rows.map((row, index) => {
                      prepareRow(row);
                      return (
                        <tr
                          key={index}
                          className={
                            index % 2 === 0 ? "bg-white" : "bg-gray-50"
                          }
                          {...row.getRowProps()}
                        >
                          {row.cells.map((cell) => {
                            return (
                              <td
                                {...cell.getCellProps()}
                                className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                              >
                                {cell.render("Cell")}
                              </td>
                            );
                          })}
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    </>
  );
};

export async function getServerSideProps() {
  const { data } = await client.query({
    query: gql`
      query MagicFormula {
        magicFormulaScore {
          symbol
          companyName
          sector
          industry
          website
          magicFormulaRank
        }
        sandp500 {
          symbol
          sector
          name
        }
      }
    `,
  });

  return {
    props: {
      data,
    },
  };
}

export default MagicFormula;
