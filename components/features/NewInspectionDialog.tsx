"use client";

import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api, type InspectionCreate } from "@/lib/api/client";

type Props = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess: (inspectionId: string) => void;
};

export function NewInspectionDialog({ open, onOpenChange, onSuccess }: Props) {
  const [name, setName] = useState("");
  const [siteLocation, setSiteLocation] = useState("");
  const [siteAddress, setSiteAddress] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const reset = () => {
    setName("");
    setSiteLocation("");
    setSiteAddress("");
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const data: InspectionCreate = {
        name: name.trim() || "Untitled inspection",
        site_location: siteLocation.trim() || null,
        site_address: siteAddress.trim() || null,
      };
      const inspection = await api.createInspection(data);
      reset();
      onSuccess(inspection.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create inspection");
    } finally {
      setSubmitting(false);
    }
  };

  const handleOpenChange = (next: boolean) => {
    if (!next) reset();
    onOpenChange(next);
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>New inspection</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="name">Inspection name</Label>
              <Input
                id="name"
                placeholder="e.g. Building 3 safety audit"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="site_location">Site location</Label>
              <Input
                id="site_location"
                placeholder="e.g. Main campus"
                value={siteLocation}
                onChange={(e) => setSiteLocation(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="site_address">Address</Label>
              <Input
                id="site_address"
                placeholder="Optional"
                value={siteAddress}
                onChange={(e) => setSiteAddress(e.target.value)}
              />
            </div>
            {error && <p className="text-sm text-destructive">{error}</p>}
          </div>
          <DialogFooter className="gap-2 sm:gap-0">
            <Button type="button" variant="outline" onClick={() => handleOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={submitting}>
              {submitting ? "Creating…" : "Create & upload files"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
