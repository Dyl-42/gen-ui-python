"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import Image from "next/image";

export interface CodeInterpreterResultProps {
  stdout?: string;
  stderr?: string;
  artifacts?: string[];
}

export function CodeInterpreterLoading(): JSX.Element {
  return (
    <Card className="w-[450px]">
      <CardHeader>
        <CardTitle>
          <Skeleton className="h-[18px] w-[100px]" />
        </CardTitle>
        <CardDescription>
          <Skeleton className="h-[14px] w-[150px]" />
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Skeleton className="h-[12px] w-full" />
        <Skeleton className="h-[12px] w-full mt-2" />
        <Skeleton className="h-[12px] w-[80%] mt-2" />
      </CardContent>
    </Card>
  );
}

export function CodeInterpreterResult(props: CodeInterpreterResultProps): JSX.Element {
  return (
    <Card className="w-[450px]">
      <CardHeader>
        <CardTitle>Code Execution Result</CardTitle>
        <CardDescription>
          {props.stdout && <span>Execution successful!</span>}
          {props.stderr && <span>Execution encountered an error.</span>}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {props.stdout && (
          <div className="mb-4">
            <h4 className="text-sm font-medium">Standard Output:</h4>
            <p className="text-muted-foreground text-sm">{props.stdout}</p>
          </div>
        )}
        {props.stderr && (
          <div className="mb-4">
            <h4 className="text-sm font-medium">Standard Error:</h4>
            <p className="text-muted-foreground text-sm">{props.stderr}</p>
          </div>
        )}
        {props.artifacts && props.artifacts.length > 0 && (
          <div className="mt-4">
            <h4 className="text-sm font-medium">Generated Artifacts:</h4>
            <div className="flex flex-wrap">
              {props.artifacts.map((artifact, index) => (
                <div key={index} className="relative w-[100px] h-[100px] m-2">
                  <Image
                    src={`/charts/${artifact}`}  // Prepend "/charts/" to the artifact filename
                    alt={`Artifact ${index + 1}`}
                    layout="fill"
                    objectFit="contain"
                    className="rounded"
                  />
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
